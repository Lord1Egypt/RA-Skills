import {sta2icon} from '/assets/v3/components/workflow.js';
export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    orders:[], //订单列表，包括自己可见的
    page:{cur:1,max:0},
    onlyMine:true
}},
created(){
    this.page.cur=this.ibf.getRt("cur",1);
    this.onlyMine=this.ibf.getRt("onlyMine",'false') == 'true';
    this.query_orders(this.page.cur);
},
methods:{
fmt_order_lines(cols, lines) {
    var orders=[];
    var dt=new Date();
    var ord,ln;
    for(var i in lines) { //id,price,skuName,creator,createAt,status,cname,cid
        ln=lines[i];
        ord={};
        for(var j in cols) {
            ord[cols[j]] = ln[j]
        }
        dt.setTime(ord.createAt*60000);
        ord.createAt=date2str(dt);
        ord.status=sta2icon(ord.status);
        orders.push(ord)
    }
    this.orders=orders;
},
query_orders(pg) {
    this.ibf.setRt("cur", pg);
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = this.onlyMine ? "/api/order/my" : "/api/order/readable";
    url += "?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK||resp.data.total==0) {
            this.orders=[];
            this.page.max=0;
            this.page.cur=1;
            return;
        }
        this.fmt_order_lines(resp.data.cols, resp.data.orders);
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
onlyMineClk() {
    this.ibf.setRt("onlyMine", this.onlyMine);
    this.page.cur=1;
    this.query_orders(1);
},
order_detail(id) {
    this.$router.push('/order?id='+id);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.home.orders}}</q-toolbar-title>
    <q-btn flat round dense icon="menu">
      <q-menu>
       <q-list style="min-width:100px">
        <q-item clickable v-close-popup>
          <q-item-section avatar>
           <q-checkbox v-model="onlyMine" @update:model-value="onlyMineClk"></q-checkbox>
          </q-item-section>
          <q-item-section>{{tags.onlyMine}}</q-item-section>
        </q-item>        
       </q-list>
     </q-menu>
    </q-btn>
   </q-toolbar>
  </q-header>

  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
  <q-pagination color="primary" v-model="page.cur" :max="page.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_contacts" dense></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.order.cname}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.order.prj}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.order.price}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.order.creator}}</q-item-label></q-item-section>
  <q-item-section thumbnail></q-item-section>
 </q-item>
 <q-item v-for="o in orders" @click="order_detail(o.id)" clickable>
  <q-item-section>{{o.cname}}</q-item-section>
  <q-item-section>{{o.prjName}}</q-icon></q-item-section>
  <q-item-section>
   <q-item-label>{{o.price}}</q-item-label>
   <q-item-label caption>{{tags.order.payment}}:{{o.payment}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{o.creator}}</q-item-label>
   <q-item-label caption>{{o.createAt}}</q-item-label>
  </q-item-section>
  <q-item-section thumbnail><q-icon :name="o.status" color="primary" size="xs"></q-icon></q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
`
}