import salesOrderCreator from './components/sales_order_creator.js';
import {completeOrder} from './components/sales_order_creator.js';

export default {
inject:['tags','service'],
components:{salesOrderCreator},
data(){return{
  orders:[],
  ctrl:{cur:1,max:0,status:-1},
  titles: [this.tags.orderNo,
      this.tags.customerName,this.tags.totalAmount,this.tags.finalAmount,
      this.tags.status,this.tags.createTime,this.tags.operation]
}},

created(){
  this.query(1);
},

methods:{
  query(pg){
    this.ctrl.cur=pg;
    var url="/api/sales/listOrders?page="+pg+"&pageSize="+this.service.PAGE_SIZE;
    if(this.ctrl.status>=0) {
        url += "&status="+this.ctrl.status;
    }
    request({method:"GET",url:url},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) {
        this.orders=[];
        this.ctrl.max=0;
        this.ctrl.cur=1;
      	return;
      }
      var dt = new Date();
      this.orders=resp.data.list.map(e => {
        dt.setTime(e.createAt);
        e.createAt = datetime2str(dt);
        e.sStatus = e.status===1?this.tags.completed:this.tags.pending
        return e;
      });
      this.ctrl.max=Math.ceil(resp.data.total/this.service.PAGE_SIZE);
    });
  },

  showCreate(){
    this.$refs.orderCreator.showCreate();
  },

  onOrderDone(isCancel){
    this.query(isCancel?this.ctrl.cur:1);
  },

  onCompleteOrder(id) {
    completeOrder(id, -1, ()=>{
      this.query(this.ctrl.cur);
    },(code, info)=>{
      this.$refs.errMsg.showErr(code,info);
    })
  },
  onStatusChanged() {
    this.query(1);
  },

  viewOrder(orderId){
    this.$refs.orderCreator.showDetail(orderId);
  }
},

template:`
<q-layout view="lHh lpr lFf" container style="height:100vh">
<q-header elevated class="bg-primary text-white">
  <q-toolbar>
    <q-btn flat icon="arrow_back" @click="$router.push('/home')"></q-btn>
    <q-toolbar-title>{{tags.salesOrder}}</q-toolbar-title>
  </q-toolbar>
</q-header>

<q-page-container>
<q-page padding>
  <div class="row items-center q-mb-md">
    <div class="text-h5">{{tags.salesOrder}}</div>
    <q-space></q-space>
    <q-select v-model="ctrl.status" :options="tags.orderStatus" @update:model-value="onStatusChanged"
     emit-value map-options class="q-px-md"></q-select>
    <q-btn color="primary" icon="add" :label="tags.createOrder" @click="showCreate"></q-btn>
  </div>

  <q-markup-table flat>
  <thead><tr>
   <th v-for="t in titles">{{t}}</th>
  </tr></thead>
  <tbody>
   <tr v-for="o in orders">
    <td class="text-left">{{o.id}}</td>
    <td>{{o.customerName}}</td>
    <td>{{o.totalAmount}}</td>
    <td>{{o.finalAmount}}</td>
    <td><q-badge :color="o.status===1?'positive':'warning'">{{o.sStatus}}</q-badge></td>
    <td>{{o.createAt}}</td>
    <td class="text-right">
     <q-btn flat dense color="primary" icon="visibility" @click="viewOrder(o.id)"></q-btn>
     <q-btn v-if="o.status===0" flat dense color="green" icon="check" @click="onCompleteOrder(o.id)"></q-btn>
    </td>
   </tr>
  </tbody>
  </q-markup-table>

  <!-- 分页 -->
  <div class="row justify-center q-mt-md" v-if="ctrl.max>1">
    <q-pagination v-model="ctrl.cur" :max="ctrl.max" :max-pages="5" @update:model-value="query"></q-pagination>
  </div>

  <!-- 创建订单对话框 -->
  <sales-order-creator ref="orderCreator" @orderCompleted="onOrderDone(false)"
   @orderCanceled="onOrderDone(true)" @hide="onOrderDone(true)"></sales-order-creator>
  <component-alert-dialog ref="errMsg"></component-alert-dialog>
</q-page>
</q-page-container>
</q-layout>
`
}
