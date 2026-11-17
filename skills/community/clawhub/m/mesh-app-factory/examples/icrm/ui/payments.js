export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    list:[], //回款列表
    page:{cur:1,max:0}
}},
created(){
    this.page.cur=this.ibf.getRt("cur",1);
    this.query_list(this.page.cur);
},
methods:{
fmt_pay_lines(cols, lines) {
    var list=[];
    var dt=new Date();
    var pm,ln;
    for(var ln of lines) { //id,amount,creator,createAt,status,customer,cname,skuName
        pm={};
        for(var i in cols) {
            pm[cols[i]]=ln[i];
        }
        dt.setTime(pm.createAt*60000);
        pm.createAt=datetime2str(dt);
        if(pm.cfmAt<=0) {
            pm.cfmAt=this.tags.payment.notCfm;
        } else {
            dt.setTime(pm.cfmAt*60000);
            pm.cfmAt=this.tags.payment.cfmAt+':'+datetime2str(dt);
        }
        list.push(pm)
    }
    this.list=list;
},
query_list(pg) {
    this.ibf.setRt("cur",pg);
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = "/api/payment/my?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK||resp.data.total==0) {
            this.list=[];
            this.page.max=0;
            this.page.cur=1;            
            return;
        }
        this.fmt_pay_lines(resp.data.cols, resp.data.payments);
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
customer_detail(id) {
    this.$router.push('/customer?id='+id);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.home.payments}}</q-toolbar-title>
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
  <q-item-section><q-item-label caption>{{tags.payment.cname}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.payment.amount}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.payment.creator}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="l in list">
  <q-item-section @click.stop="customer_detail(l.customer)">{{l.cname}}</q-item-section>
  <q-item-section>
   <q-item-label>{{l.amount}}</q-item-label>
   <q-item-label caption>{{l.cfmAt}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{l.creator}}</q-item-label>
   <q-item-label caption>@{{l.createAt}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
`
}