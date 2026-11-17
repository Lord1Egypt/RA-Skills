import salesOrderCreator from './components/sales_order_creator.js';
import {completeOrder, cancelOrder} from './components/sales_order_creator.js';

export default {
inject:['tags','service'],
components:{salesOrderCreator},
data(){return{
  stats:{},
  isOwner:false,
  canPurchase:false,
  canSales:false,
  recentOrders:[],
  salesTrendData:[],
  lowStock:[]
}},

created(){
    var url="/power/get?service="+this.service.name;
    request({method:"GET",url:url}, SERVICE_USER).then(resp=>{
        if(resp.code!=0) {
            Console.warn("request "+url+" failed:" + resp.code + ",info:" + resp.info);
            return;
        }
        var role=resp.data.role;
        this.isOwner=role=='admin';
        this.canPurchase=(role=='admin'||role=='purchaser');
        this.canSales=(role=='admin'||role=='salesperson');
    });
    this.loadStats();
    this.loadLowStock();
    //销售与客户管理对所有角色开放，首页最近订单直接加载
    this.loadRecentOrders();
},

methods:{
  loadLowStock(){
    request({method:"GET",url:"/api/report/lowStockList?limit=10"},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){this.lowStock=[];return;}
      this.lowStock=resp.data.list||[];
    });
  },

  loadStats(){
    var end=Date.now();
    var start=end - 7 * 86400 * 1000;
    var url="/api/report/stats?startDate="+start+"&endDate="+end;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) return;
      this.stats=resp.data;
    });
  },

  loadRecentOrders(){
    request({method:"GET",url:"/api/sales/listOrders?page=1&pageSize=5"},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) {
        this.recentOrders=[];
        return;
      }
      var dt = new Date();
      this.recentOrders=resp.data.list.map(e =>{
        dt.setTime(e.createAt);
        e.createAt = datetime2str(dt);
        e.sStatus = e.status===1?this.tags.completed:this.tags.pending
        return e;
      });
    });
  },

  showCreateSalesOrder(){
    this.$refs.salesOrderCreator.showCreate();
  },

  onSalesOrderDone(ignore){
    if(!ignore) {
        this.loadStats();
    }
    this.loadRecentOrders();
  },

  viewOrder(id){
    this.$refs.salesOrderCreator.showDetail(id);
  },

  onCompleteOrder(id) {
    completeOrder(id, -1, ()=>{
      this.loadStats();
      this.loadRecentOrders();
    },(code, info)=>{
      this.$refs.errMsg.showErr(code,info);
    })
  }
},

template:`
<q-layout view="lHh lpr lFf" container style="height:100vh">
<q-header elevated class="bg-primary text-white">
  <q-toolbar>
    <q-toolbar-title>{{tags.app_name}}</q-toolbar-title>
    <q-btn-dropdown flat icon="menu" :label="tags.more">
      <q-list>
        <q-item clickable @click="$router.push('/products')" v-if="canPurchase">
          <q-item-section avatar><q-icon name="inventory_2"></q-icon></q-item-section>
          <q-item-section>{{tags.products}}</q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/suppliers')" v-if="canPurchase">
          <q-item-section avatar><q-icon name="business"></q-icon></q-item-section>
          <q-item-section>{{tags.suppliers}}</q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/customers')">
          <q-item-section avatar><q-icon name="people"></q-icon></q-item-section>
          <q-item-section>{{tags.customers}}</q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/categories')" v-if="canPurchase">
          <q-item-section avatar><q-icon name="category"></q-icon></q-item-section>
          <q-item-section>{{tags.categories}}</q-item-section>
        </q-item>
        <q-separator></q-separator>
        <q-item clickable @click="$router.push('/purchase')" v-if="canPurchase">
          <q-item-section avatar><q-icon name="shopping_cart"></q-icon></q-item-section>
          <q-item-section>{{tags.purchase}}</q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/sales')">
          <q-item-section avatar><q-icon name="point_of_sale"></q-icon></q-item-section>
          <q-item-section>{{tags.sales}}</q-item-section>
        </q-item>
        <q-separator></q-separator>
        <q-item clickable @click="$router.push('/reports')" v-if="isOwner">
          <q-item-section avatar><q-icon name="assessment"></q-icon></q-item-section>
          <q-item-section>{{tags.reports}}</q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </q-toolbar>
</q-header>

<q-page-container>
<q-page padding>
  <!-- 统计卡片 -->
  <div class="row q-col-gutter-md q-mb-md">
    <div class="col-12 col-sm-6 col-md-3">
      <q-card class="bg-primary text-white">
        <q-card-section>
          <div class="text-h6">{{tags.todaySales}}</div>
          <div class="text-h4">¥{{stats.todaySales||0}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card class="bg-secondary text-white">
        <q-card-section>
          <div class="text-h6">{{tags.monthSales}}</div>
          <div class="text-h4">¥{{stats.monthSales||0}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card class="bg-positive text-white">
        <q-card-section>
          <div class="text-h6">{{tags.productCount}}</div>
          <div class="text-h4">{{stats.productCount||0}}</div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
      <q-card :class="stats.lowStockCount>0?'bg-negative text-white':'bg-info text-white'">
        <q-card-section>
          <div class="text-h6">{{tags.lowStockAlert}}</div>
          <div class="text-h4">{{stats.lowStockCount||0}}</div>
        </q-card-section>
      </q-card>
    </div>
  </div>

  <!-- 最近订单 -->
  <q-card class="q-mb-md">
    <q-card-section class="row items-center">
      <div class="text-h6">{{tags.recentOrders}}</div>
      <q-space></q-space>
      <q-btn flat color="primary" icon="point_of_sale" :label="tags.sales" @click="$router.push('/sales')"></q-btn>
      <q-btn flat color="primary" icon="add_shopping_cart" :label="tags.createSalesOrder" @click="showCreateSalesOrder"></q-btn>
    </q-card-section>
    <q-card-section>
      <q-table :rows="recentOrders" :columns="[
        {name:'id',label:tags.orderNo,field:'id'},
        {name:'customerName',label:tags.customerName,field:'customerName'},
        {name:'finalAmount',label:tags.finalAmount,field:'finalAmount'},
        {name:'status',label:tags.status,field:'sStatus'},
        {name:'createAt',label:tags.createTime,field:'createAt'},
        {name:'action',label:tags.operation,field:'action'}
      ]" row-key="id" flat dense hide-bottom>
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-badge :color="props.row.status===1?'positive':'warning'">
              {{props.row.sStatus}}
            </q-badge>
          </q-td>
        </template>
        <template v-slot:body-cell-action="props">
          <q-td :props="props">
            <q-btn flat dense color="primary" icon="visibility" @click="viewOrder(props.row.id)"></q-btn>
            <q-btn v-if="props.row.status===0" flat dense color="green" icon="check" @click="onCompleteOrder(props.row.id)"></q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card-section>
  </q-card>

  <!-- 低库存预警 -->
  <q-card class="q-mb-md">
    <q-card-section class="row items-center">
      <div class="text-h6 text-negative">{{tags.lowStockList}}</div>
      <q-space></q-space>
      <q-btn flat color="primary" icon="inventory_2" :label="tags.products" @click="$router.push('/products')"></q-btn>
    </q-card-section>
    <q-card-section>
      <q-list bordered separator v-if="lowStock.length>0">
        <q-item v-for="p in lowStock" :key="p.id">
          <q-item-section>
            <q-item-label>{{p.name}}</q-item-label>
            <q-item-label caption>{{p.categoryName}} / {{p.unit}}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-badge color="negative">{{tags.stock}}: {{p.stock}} / {{p.minStock}}</q-badge>
          </q-item-section>
        </q-item>
      </q-list>
      <div v-else class="text-grey">{{tags.noData}}</div>
    </q-card-section>
  </q-card>

  <sales-order-creator ref="salesOrderCreator" @orderCompleted="onSalesOrderDone(false)"
   @orderCanceled="onSalesOrderDone(false)" @hide="onSalesOrderDone(true)"></sales-order-creator>
</q-page>
</q-page-container>
</q-layout>

<component-alert-dialog ref="errMsg"></component-alert-dialog>
`
}
